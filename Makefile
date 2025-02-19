.PHONY: clean clean-venv venv install validate build deploy-local deploy set-webhook show-results test
AWS_REGION ?= eu-west-3
AWS_PROFILE ?= "esgis_profile"

clean:
	rm -rf build .coverage .python-version *egg-info .pytest_cache

clean-venv:
	rm -rf .venv

venv: clean-venv clean
	python3 -m venv .venv

install:
	@echo "Installing dependencies for " ${environment}
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
validate:
	sam validate -t infrastructure/template.yaml --lint

build:
	sam build --use-container -t infrastructure/template.yaml

deploy-local:
	sam local start-api

serve:
	.venv/bin/fastapi dev src/main.py

deploy:
	@echo "Deploying to " ${env}
	sam deploy --resolve-s3 --template-file .aws-sam/build/template.yaml --stack-name pethaul-stack-${env} \
         --capabilities CAPABILITY_IAM --region ${AWS_REGION} --parameter-overrides EnvironmentName=${env} TelegramToken=${TELEGRAM_BOT_TOKEN} MistalApiKey=${MISTRAL_API_KEY} --no-fail-on-empty-changeset --profile ${AWS_PROFILE}

set-webhook:
	curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${URL}"

show-results:
	aws cloudformation describe-stacks \
		--stack-name "pethaul-stack-${env}" \
		--region ${AWS_REGION} \
		--query 'Stacks[0].Outputs[?OutputKey==`DynamoDBTableName`].OutputValue' --output text
	aws cloudformation describe-stacks \
		--stack-name "pethaul-stack-${env}" \
		--region ${AWS_REGION} \
		--query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text

test:
	@echo "Running tests..."
	.venv/bin/pytest