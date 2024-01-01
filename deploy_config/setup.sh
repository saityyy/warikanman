WORKDIR="/home/ubuntu/warikanman/deploy_config"
cp ${WORKDIR}/nginx/default /etc/nginx/sites-available/default
cp ${WORKDIR}/env/linebot_env.sh ~/linebot_env.sh
cp ${WORKDIR}/systemd/warikanman.service ~/.config/systemd/user/warikanman.service

