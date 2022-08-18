resource "aws_sfn_state_machine" "pred_state_machine" {
  name       = var.pred_state_machine_name
  role_arn   = aws_iam_role.step_function_lambda_invole_role.arn
  definition = data.local_file.train_step_function_file.content
}

data "local_file" "train_step_function_file" {
  filename = "./data/step_functions/pred_step_function.json"
}
