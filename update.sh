git add . --all
git commit -m $1
git push

expect "Username for 'https://github.com':"
send "mac389"