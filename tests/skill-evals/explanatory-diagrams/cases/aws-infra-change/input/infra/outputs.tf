output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "db_endpoint" {
  value = aws_db_instance.main.address
}

output "product_images_bucket" {
  value = aws_s3_bucket.product_images.bucket
}

output "product_images_domain" {
  value = aws_cloudfront_distribution.product_images.domain_name
}
