from fabric.api import local

def test_cov():
	local('python manage.py jenkins --coverage-html-report=htmlcov')

def deploy():
	# Push changes to master
	local("git push origin master")

	# Push changes to Heroku
	local("git push heroku master")

	# Run migrations on Heroku
	local("heroku run python manage.py migrate")
