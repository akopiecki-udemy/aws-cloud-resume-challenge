resource "aws_lambda_function" "myfunc" {
  filename         = data.archive_file.zip_the_python_code.output_path
  source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
  function_name    = "resumefunc"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "resumefunc.lambda_handler"
  runtime          = "python3.8"
  timeout          = 10
}