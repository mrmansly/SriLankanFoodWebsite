This is a side project I have developed to help with show casing my UI/UX skills and improve my skills in newer technologies.
It is constantly evolving with the latest additions being Selenium functional tests.

Future Roadmap:
- Docker Containerisation
- User Account and Login process
- Microservice Architecture
- Serverless Architecture

<p>
Feel free to access the URL (http://3.107.102.106) and play around by making orders and leaving any feedback!<br>
</p>
<b>
WARNING: The site is secured with a self signed certificate, allowing for https. However, as it is using a self signed certificate, you will get a warning as you 
enter the site saying it is insecure. It is ok to proceed onto the beta website regardless. A proper CA certificate will be obtained for a production ready URL.
</b>
<br>
<br>

The following notes are instructions for the EC2 deployment, which will soon be handled as part of a docker container.

//Update the Ubuntu Image<br>
sudo apt-get update

//Clone GIT Repo<br>
git clone https://github.com/mrmansly/SriLankanFoodWebsite.git

// CD into project<br>
cd SriLankanFoodWebsite

// Download Python/PIP and virtual environment<br>
sudo apt install python3-venv python3-pip -y

// Create the virtual environment<br>
python3 -m venv myenv

// Activate the virtual environment<br>
source myenv/bin/activate

// Download Django<br>
pip install django

// Download Bootstrap5<br>
pip install django-bootstrap5

// Download sass processor<br>
// for prod we should only need sass-processor I believe.<br>
//pip install libsass django-compressor django-sass-processor<br>  
pip install libsass django-sass-processor

// Download rest framework<br>
pip install djangorestframework

// Make migrations - NOTE: Warning about css file not existing in STATICFILES_DIRS  (collectstaticfiles)<br>
python3 manage.py makemigrations
<br>
python3 manage.py migrate

// NOTE: First time I ran this it required a directory to exist. When I checked the css directory did already exist, so<br>
// ran this again, and this time it was successful. When should this be getting called?<br>
python3 manage.py collectstatic<br>

// Set allowed host to Public IP address of EC2 container<br>
DJANGO_ALLOWED_HOSTS='3.107.102.106' python3 manage.py runserver 0.0.0.0:8000


