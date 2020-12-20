for story in $(cat ../urls.txt)
do
    echo "$story"
    wget "$story"
    sleep 5
done