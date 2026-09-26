resource "aws_cloudfront_origin_access_control" "product_images" {
  name                              = "${var.name}-product-images"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

data "aws_cloudfront_cache_policy" "caching_optimized" {
  name = "Managed-CachingOptimized"
}

# EC の商品ページと管理画面は、このドメインから画像を読む
resource "aws_cloudfront_distribution" "product_images" {
  enabled         = true
  comment         = "${var.name} product images"
  is_ipv6_enabled = true
  price_class     = "PriceClass_200"

  origin {
    origin_id                = "product-images"
    domain_name              = aws_s3_bucket.product_images.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.product_images.id
  }

  default_cache_behavior {
    target_origin_id       = "product-images"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = data.aws_cloudfront_cache_policy.caching_optimized.id
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
