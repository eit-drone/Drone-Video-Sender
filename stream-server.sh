while :
do
  echo " ########################### "
  echo ""
  echo "  Launching RTMP server..."
  echo ""
  echo " ########################### "
  
  ffmpeg -f flv -listen 1 -i ${1:-rtmp://172.20.10.12:8889/live/app} -c copy -f flv -listen 1 ${2:-rtmp://localhost:1935/live/app}
  
  echo " ########################### "
  echo ""
  echo "  RTMP stream ended. Restarting in 3 seconds..."
  echo ""
  echo " ########################### "
  sleep 3
done
