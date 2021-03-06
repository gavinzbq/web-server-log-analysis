# Table of Contents
1. [Abstract](README.md#abstract)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Description of Data](README.md#description-of-data)
4. [Result](README.md#result)


# Abstract
The work here is to perform basic analytics on the server log file, provide useful metrics, and implement basic security measures. This dataset is inspired by real NASA web traffic, which is very similar to server logs from e-commerce and other sites. Monitoring web traffic and providing these analytics is a real business need.

The feature support are described below: 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

### New Feature:
List the top 10 busiest (most frequently visited) 1-hour window whose start time is exactly at the beginning of an hour, i.e. '[DD/MON/YYYY:HH:00:00 -0400]'.

### Dependency:
Python 2.7


## Details of Implementation

### Feature 1 
List in descending order the top 10 most active hosts/IP addresses that have accessed the site.

Write to a file, named `hosts.txt`, the 10 most active hosts/IP addresses in descending order and how many times they have accessed any part of the site. There should be at most 10 lines in the file, and each line should include the host (or IP address) followed by a comma and then the number of times it accessed the site. 

e.g., `hosts.txt`:

    example.host.com,1000000
    another.example.net,800000
    31.41.59.26,600000
    …


### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth. Bandwidth consumption can be extrapolated from bytes sent over the network and the frequency by which they were accessed.

These most bandwidth-intensive resources, sorted in descending order and separated by a new line, should be written to a file called `resources.txt`


e.g., `resources.txt`:
    
    /images/USA-logosmall.gif
    /shuttle/resources/orbiters/discovery.html
    /shuttle/countdown/count.html
    …


### Feature 3 
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period.

Write to a file named `hours.txt`, the start of each 60-minute window followed by the number of times the site was accessed during that time period. The file should contain at most 10 lines with each line containing the start of each 60-minute window, followed by a comma and then the number of times the site was accessed during those 60 minutes. The 10 lines should be listed in descending order with the busiest 60-minute window shown first. 

e.g., `hours.txt`:

    01/Jul/1995:00:00:01 -0400,100
    02/Jul/1995:13:00:00 -0400,22
    05/Jul/1995:09:05:02 -0400,10
    01/Jul/1995:12:30:05 -0400,8
    …

Note: A 60-minute window can be any 60 minute long time period, windows don't have to start at a time when an event occurs.

### Feature 4 
Feature 4 is to detect patterns of three consecutive failed login attempts over 20 seconds in order to block all further attempts to reach the site from the same IP address for the next 5 minutes. Each attempt that would have been blocked should be written to a log file named `blocked.txt`.

The site’s fictional owners don’t expect you to write the actual web server code to block the attempt, but rather want to gauge how much of a problem these potential security breaches represent. 

Detect three failed login attempts from the same IP address over a consecutive 20 seconds, and then write to the `blocked.txt` file any subsequent attempts to reach the site from the same IP address over the next 5 minutes. 

For example, if the third consecutive failed login attempt within a 20 second window occurred on `01/Aug/1995:00:00:08`, all access to the website for that IP address would be blocked for the next 5 minutes. Even if the same IP host attempted a login -- successful or not -- one minute later at `01/Aug/1995:00:01:08`, that attempt should be ignored and logged to the `blocked.txt` file. Access to the site from that IP address would be allowed to resume at `01/Aug/1995:00:05:09`.

If an IP address has not reached three failed login attempts during the 20 second window, a login attempt that succeeds during that time period should reset the failed login counter and 20-second clock. 

For example, if after two failed login attempts, a third login attempt is successful, full access should be allowed to resume immediately afterward. The next failed login attempt would be counted as 1, and the 20-second timer would begin there. In other words, this feature should only be triggered if an IP has  3 failed logins in a row, within a 20-second window.

e.g., `blocked.txt`

    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    …

The following illustration may help you understand how this feature might work, and when three failed login attempts would trigger 5 minutes of blocking:


![Feature 4 illustration](images/feature4.png)


Note that this feature should not impact the other features in this challenge. For instance, any requests that end up in the `blocked.txt` file should be counted toward the most active IP host calculation, bandwidth consumption and busiest 60-minute period.

### New feature
The additional feature here is to list the top 10 busiest (most frequently visited) 1-hour window whose start time is exactly at the beginning of an hour.

Write to a file named `busyhr.txt`, the start of each 60-minute window followed by the number of times the site was accessed during that time period. The file should contain at most 10 lines with each line containing the start of each 60-minute window, followed by a comma and then the number of times the site was accessed during those 60 minutes. The 10 lines should be listed in descending order. 

e.g., `busyhr.txt`:

    01/Jul/1995:00:00:00 -0400,100
    02/Jul/1995:13:00:00 -0400,22
    05/Jul/1995:09:00:00 -0400,10
    01/Jul/1995:12:00:00 -0400,8
    …


## Description of Data

You can download the data here: https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view

Assume you receive as input, a file, `log.txt`, in ASCII format with one line per request, containing the following columns:

* **host** making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.

* **timestamp** in the format `[DD/MON/YYYY:HH:MM:SS -0400]`, where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.

* **request** given in quotes.

* **HTTP reply code**

* **bytes** in the reply. Some lines in the log file will list `-` in the bytes field. For the purposes of this challenge, that should be interpreted as 0 bytes.


e.g., `log.txt`

    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -400] "POST /login HTTP/1.0" 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -400] "POST /login HTTP/1.0" 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    ...
    
In the above example, the 2nd line shows a failed login (HTTP reply code of 401) followed by a successful login (HTTP reply code of 200) two seconds later from the same IP address.

## Result

### Feature 1

The top 10 hosts / IP are as following.

    piweba3y.prodigy.com,22096
    piweba4y.prodigy.com,14785
    piweba1y.prodigy.com,12730
    siltb10.orl.mmc.com,10568
    alyssa.prodigy.com,10092
    edams.ksc.nasa.gov,9046
    piweba2y.prodigy.com,7897
    163.206.89.4,6475
    www-d3.proxy.aol.com,6212
    vagrant.vf.mmc.com,6074

### Feature 2

The top 10 resources with the most bandwidth consumption as following.

    /shuttle/missions/sts-71/movies/sts-71-launch.mpg
    /
    /shuttle/missions/sts-71/movies/sts-71-tcdt-crew-walkout.mpg
    /shuttle/missions/sts-53/movies/sts-53-launch.mpg
    /shuttle/countdown/count70.gif
    /shuttle/technology/sts-newsref/stsref-toc.html
    /shuttle/countdown/video/livevideo2.gif
    /shuttle/countdown/count.gif
    /shuttle/countdown/video/livevideo.gif
    /shuttle/missions/sts-71/movies/sts-71-mir-dock.mpg

### Feature 3

The top 10 busiest (most frequently visited) 60-minute periods.

    13/Jul/1995:08:59:33 -0400,34881
    13/Jul/1995:08:59:39 -0400,34872
    13/Jul/1995:08:59:40 -0400,34872
    13/Jul/1995:08:59:35 -0400,34869
    13/Jul/1995:08:59:34 -0400,34868
    13/Jul/1995:08:59:41 -0400,34866
    13/Jul/1995:08:59:42 -0400,34864
    13/Jul/1995:08:59:36 -0400,34862
    13/Jul/1995:08:59:37 -0400,34860
    13/Jul/1995:08:59:38 -0400,34860


        
It is observed that the top 10 busiest 1-hour window gather within a 1-minute time period. 10 lines of results conclude basically one busiest 1-hour window. It is the primary motivation to add the new feature.

### Feature 4

Too long.

### New feature

The top 10 busiest hours are as following.

    13/Jul/1995:09:00:00 -0400,34817
    13/Jul/1995:08:00:00 -0400,26978
    13/Jul/1995:10:00:00 -0400,23787
    13/Jul/1995:11:00:00 -0400,22600
    13/Jul/1995:12:00:00 -0400,19857
    05/Jul/1995:14:00:00 -0400,18694
    13/Jul/1995:14:00:00 -0400,17390
    13/Jul/1995:13:00:00 -0400,17016
    13/Jul/1995:15:00:00 -0400,16925
    05/Jul/1995:16:00:00 -0400,16742
    
The new feature is practical when the log file records traffic through several days or more. Compared with feature 3, it has advantage that much less amount of data needs to be generated and processed.