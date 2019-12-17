for file in *.png ; do 
	cwebp -q 75 "$file" -o "${file%.png}.webp";
done