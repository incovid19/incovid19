#!/usr/bin/env bash

curl -c cookies.txt \
     -o kerala-index.html https://dashboard.kerala.gov.in/covid/index.php

curl --referer "https://dashboard.kerala.gov.in/covid/index.php" \
     -b cookies.txt \
     -c new_cookies.txt \
     -o kerala-districts.html https://dashboard.kerala.gov.in/covid/dailyreporting-view-public-districtwise.php
     
curl --referer "https://dashboard.kerala.gov.in/covid/index.php" \
     -b cookies.txt \
     -c new_cookies.txt \
     -o kerala-testing.html https://dashboard.kerala.gov.in/covid/testing-view-public.php

for CODE in {1601..1614}; do
    echo "Downloading for district=$CODE";
    mv new_cookies.txt cookies.txt
    curl -X POST \
	 --referer "https://dashboard.kerala.gov.in/covid/index.php" \
	 -b cookies.txt \
	 -c new_cookies.txt \
	 -F district=${CODE} \
	 -o "kerala-${CODE}.html" https://dashboard.kerala.gov.in/covid/dailyreporting-view-public-districtwise.php
done