while :
do
  echo " ########################### "
  echo ""
  echo "  Launching RTMP server..."
  echo "    RTMP in: ${1:-rtmp://localhost:8889/live/app}"
  echo "    RTMP out: ${2:-rtmp://localhost:1935/live/app}"
  echo ""
  echo " ########################### "
  
  ffmpeg -f live_flv -listen 1 -i ${1:-rtmp://localhost:8889/live/app} -c copy -f flv -listen 1 ${2:-rtmp://localhost:1935/live/app} -loglevel debug
  
  echo " ########################### "
  echo ""
  echo "  RTMP stream ended. Restarting in 3 seconds..."
  echo ""
  echo " ########################### "
  sleep 3
done
