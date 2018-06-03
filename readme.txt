t is a version control system.
Git is free software.

git add 
git commit -m "自定义描述"

git checkout -- readme.txt
git reset HEAD readme.txt

git remote add origin git@github.com:srp527/Mxonline362.git  
git push -u origin master
git push origin master

git clone git@github.com:srp527/Mxonline362.git


1.在本地目录下关联远程repository ：
  git remote add origin git@github.com:git_username/repository_name.git



2.取消本地目录下关联的远程库：
  git remote remove origin


3.git无法pull仓库refusing to merge unrelated histories
  git pull origin master --allow-unrelated-histories
