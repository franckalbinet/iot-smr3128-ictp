#/bin/bash

# Copy folders
cp -R ../labs smr3128-material/
cp -R ../python-fundamentals smr3128-material/
cp -R ../softs smr3128-material/
echo "Files copied successfully!"

# Create archive
now=`date +"%Y%m%d"`
zip -r smr3128-material-$now.zip smr3128-material
echo "Material zipped successfully!"
