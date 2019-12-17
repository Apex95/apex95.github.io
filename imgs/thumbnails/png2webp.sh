for file in *.jpeg ; do 
	cwebp -q 75 "$file" -o "${file%.jpeg}.webp";
done