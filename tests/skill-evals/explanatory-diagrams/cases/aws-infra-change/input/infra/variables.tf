variable "region" {
  type    = string
  default = "ap-northeast-1"
}

variable "name" {
  description = "リソース名の接頭辞"
  type        = string
  default     = "shop"
}

variable "api_image" {
  description = "API のコンテナイメージ（ECR の URI とタグ）"
  type        = string
}

variable "certificate_arn" {
  description = "api.example.com の証明書（ACM）。api.example.com は ALB を指す"
  type        = string
}

variable "admin_origin" {
  description = "管理画面のオリジン。ブラウザから S3 へのアップロードを CORS で許す"
  type        = string
  default     = "https://admin.example.com"
}
