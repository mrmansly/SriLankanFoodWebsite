This is a side project I have developed to help with show casing my UI/UX skills and improve my skills in newer technologies.

Feel free to access the URL and play around by making orders and leaving any feedback!

The following notes are instructions for the EC2 deployment, which will soon be handled as part of a docker container.

//Update the Ubuntu Image
sudo apt-get update

//Clone GIT Repo
git clone https://github.com/mrmansly/SriLankanFoodWebsite.git

// CD into project
cd SriLankanFoodWebsite

// Download Python/PIP and virtual environment
sudo apt install python3-venv python3-pip -y

// Create the virtual environment
python3 -m venv myenv

// Activate the virtual environment
source myenv/bin/activate

// Download Django
pip install django

// Download Bootstrap5
pip install django-bootstrap5

// Download sass processor
// for prod we should only need sass-processor I believe.
//pip install libsass django-compressor django-sass-processor  
pip install libsass django-sass-processor

// Download rest framework
pip install djangorestframework

// Make migrations - NOTE: Warning about css file not existing in STATICFILES_DIRS  (collectstaticfiles)
python3 manage.py makemigrations

python3 manage.py migrate

// NOTE: First time I ran this it required a directory to exist. When I checked the css directory did already exist, so
// ran this again, and this time it was successful. When should this be getting called?
python3 manage.py collectstatic

// Set allowed host to Public IP address of EC2 container
DJANGO_ALLOWED_HOSTS='3.107.102.106' python3 manage.py runserver 0.0.0.0:8000


