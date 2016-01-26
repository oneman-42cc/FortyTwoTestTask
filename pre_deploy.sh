ls
python manage.py migrate

cd static && ls && cd ..
rm -rf static/*

tree -p ../uploads
rm -f ../uploads/*.png
