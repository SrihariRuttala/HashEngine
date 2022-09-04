#!/bin/bash

echo "# HashEngine" >> README.md
git init
git add .
git commit -m "Push source"
git branch -M main
git remote add origin git@github.com:SrihariRuttala/HashEngine.git
git push -u origin main
