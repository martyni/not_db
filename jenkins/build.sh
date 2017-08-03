virtualenv env
source env/bin/activate
for req in $(cat requirements.txt) 
   do pip install $req --upgrade
done	   
pip install . --upgrade
