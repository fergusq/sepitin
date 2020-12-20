for story in stories/*.html
do
    id=$(cat "$story" | hxnormalize -x | hxselect -i '#preface > .message > a:nth-of-type(2)' | sed -E 's/<[^>]+>//g;s!http://archiveofourown.org/works/!!')
    name=$(cat "$story" | hxnormalize -x | hxselect -i '#preface > .message > b' | sed -E 's/<[^>]+>//g' | tr '\n' ' ')
    author=$(cat "$story" | hxnormalize -x | hxselect -i '.byline a[rel=author]' | sed -E 's/<[^>]+>//g' | tr '\n' ' ')
    echo "$id: $name, tekijä $author" >&2
    echo "### id: $id"
    echo "### nimi: $name"
    echo "### tekijä: $author"
    cat "$story" | hxnormalize -x | hxselect -i '#preface > .meta > blockquote:first-of-type, #chapters' | hxremove -i '.meta.group :not(:first-child), #chapters .meta:not(.group)' | pandoc -f html -t plain
done