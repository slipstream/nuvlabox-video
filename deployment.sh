#!/bin/bash -xe

# Case insensitive comparaison (for "case" and "[[ ]]" conditions)
shopt -s nocasematch

# set url
port=5000
#hostname="$(ss-get hostname)"
#cloudservice="$(ss-get cloudservice)"
#quality="$(ss-get --noblock quality)"
#width="$(ss-get --noblock width)"
#height="$(ss-get --noblock height)"
#threads="$(ss-get --noblock threads)"
#bad_connection="$(ss-get --noblock bad_connection)"

: ${quality:=80}
: ${width:=640}
: ${height:=480}
: ${threads:=4}
: ${bad_connection:='False'}

#ss-display 'Deploying faces'
cat << EOF > /usr/lib/systemd/system/faces.service
[Unit]
Description=Faces App
After=network.target

[Service]
User=root
ExecStart=/root/nuvlabox-video/app.py ${quality} ${width} ${height} ${threads}
ExecStop=/bin/kill -TERM \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

if [[ $bad_connection == True ]]; then
    echo '4096 8192 16384' > /proc/sys/net/ipv4/tcp_wmem
fi

#ss-display 'Starting Faces'
systemctl daemon-reload
systemctl enable faces.service
systemctl start faces.service

local_url="http://${hostname}:${port}"
#ss-set url.service.local "$local_url"

if [[ $cloudservice == nuvlabox-* ]]; then
    nuvlabox_name=${cloudservice#nuvlabox-}
    IFS=. read ip1 ip2 ip3 ip4 <<< "$hostname"
    vm_number="${ip4}"
    remote_url="https://vm${vm_number}-${port}.${nuvlabox_name}.nuvlabox.com/video"
    url="$remote_url"
    #ss-set url.service.remote "$remote_url"
else
    url="$local_url"
fi

#ss-set url.service "$url"
#ss-set ss:url.service "$url"

#ss-display 'Faces ready'
