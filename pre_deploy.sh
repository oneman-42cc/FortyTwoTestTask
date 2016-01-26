ls
python manage.py migrate --delete-ghost-migrations

cd static && ls && cd ..
rm -rf static/*

tree -p ../uploads
rm -f ../uploads/*.png
