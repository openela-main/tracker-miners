#! /bin/sh

set -eu

app=$1

for srv in Files Files.Control; do
    sed -e "s|org.gnome.FlatpakApp|${app}|" -i /app/share/dbus-1/services/org.gnome.FlatpakApp.Tracker3.Miner.$srv.service ;
    mv /app/share/dbus-1/services/{org.gnome.FlatpakApp,${app}}.Tracker3.Miner.$srv.service ;
done

sed -e "s|org.gnome.FlatpakApp|${app}|" -i /app/share/tracker3/domain-ontologies/org.gnome.FlatpakApp.domain.rule
mv /app/share/tracker3/domain-ontologies/{org.gnome.FlatpakApp,${app}}.domain.rule
