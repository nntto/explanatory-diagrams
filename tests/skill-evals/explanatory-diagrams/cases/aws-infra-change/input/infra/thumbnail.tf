locals {
  # functions/thumbnail を CI でビルドした zip
  thumbnail_package = "${path.module}/build/thumbnail.zip"
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "thumbnail" {
  name               = "${var.name}-thumbnail"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "thumbnail_logs" {
  role       = aws_iam_role.thumbnail.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "thumbnail" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.product_images.arn}/originals/*"]
  }

  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.product_images.arn}/thumbnails/*"]
  }
}

resource "aws_iam_role_policy" "thumbnail" {
  name   = "product-images"
  role   = aws_iam_role.thumbnail.id
  policy = data.aws_iam_policy_document.thumbnail.json
}

resource "aws_cloudwatch_log_group" "thumbnail" {
  name              = "/aws/lambda/${var.name}-thumbnail"
  retention_in_days = 30
}

# originals/<キー> を読み、幅 400px に縮めて thumbnails/<キー> に置く
resource "aws_lambda_function" "thumbnail" {
  function_name    = "${var.name}-thumbnail"
  role             = aws_iam_role.thumbnail.arn
  runtime          = "nodejs22.x"
  handler          = "index.handler"
  architectures    = ["arm64"]
  filename         = local.thumbnail_package
  source_code_hash = filebase64sha256(local.thumbnail_package)
  memory_size      = 1024
  timeout          = 30

  environment {
    variables = {
      THUMBNAIL_PREFIX = "thumbnails/"
      THUMBNAIL_WIDTH  = "400"
    }
  }

  depends_on = [aws_cloudwatch_log_group.thumbnail]
}

resource "aws_lambda_permission" "thumbnail_from_s3" {
  statement_id   = "AllowInvokeFromProductImages"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.thumbnail.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.product_images.arn
  source_account = data.aws_caller_identity.current.account_id
}
