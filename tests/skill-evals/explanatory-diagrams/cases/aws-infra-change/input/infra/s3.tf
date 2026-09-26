data "aws_caller_identity" "current" {}

# 元の画像は originals/、サムネイルは thumbnails/ に置く
resource "aws_s3_bucket" "product_images" {
  bucket = "${var.name}-product-images-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_public_access_block" "product_images" {
  bucket = aws_s3_bucket.product_images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 管理画面から、署名付き URL で直接 PUT する
resource "aws_s3_bucket_cors_configuration" "product_images" {
  bucket = aws_s3_bucket.product_images.id

  cors_rule {
    allowed_methods = ["PUT"]
    allowed_origins = [var.admin_origin]
    allowed_headers = ["Content-Type"]
    max_age_seconds = 3000
  }
}

# 読めるのは CloudFront（OAC）だけ
data "aws_iam_policy_document" "product_images_bucket" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.product_images.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.product_images.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "product_images" {
  bucket = aws_s3_bucket.product_images.id
  policy = data.aws_iam_policy_document.product_images_bucket.json

  depends_on = [aws_s3_bucket_public_access_block.product_images]
}

# originals/ に置かれた画像だけを Lambda に渡す。
# thumbnails/ は対象にしないので、Lambda が置いたサムネイルで Lambda がまた動くことはない
resource "aws_s3_bucket_notification" "product_images" {
  bucket = aws_s3_bucket.product_images.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.thumbnail.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "originals/"
  }

  depends_on = [aws_lambda_permission.thumbnail_from_s3]
}
