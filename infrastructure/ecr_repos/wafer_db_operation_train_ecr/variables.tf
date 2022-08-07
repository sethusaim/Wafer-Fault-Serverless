variable "wafer_db_operation_train_ecr_name" {
  default = "wafer_db_operation_train"
  type    = string
}

variable "image_tag_mutability" {
  default = "MUTABLE"
  type    = string
}

variable "scan_on_push" {
  default = true
  type    = bool
}