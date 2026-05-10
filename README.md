# opnsense-ip66
Skript for converting ip66.dev geoip database to a CSV format suitable for OpnSense


You can run this on any server using python3 with an installed maxminddb package (pip install maxminddb) like so:

python3 opnsense-ip66.py

You should modify the TARGET_GZIP to the path your webserver can serve. Also note that in order for your webserver to serve the file correctly,
it must hand out a "Content-Disposition" HTTP header. For NGinx, this can be done like so:

location ~* \.gz$ {
    # Extrahiert den Dateinamen aus dem Pfad (z.B. "ipinfo_lite.csv.gz")
    if ($request_filename ~* ^.*/(.+\.gz)$ ) {
        set $filename $1;
    }

    # Setzt den Header, den OPNsense benötigt, um nicht auf .zip zurückzufallen
    add_header Content-Disposition 'attachment; filename="$filename"';

    # Wichtig: Den korrekten MIME-Type mitsenden
    types { }
    default_type application/gzip;
}

and for Apache, like so:

<FilesMatch "\.gz$">
    # Extrahiert den Dateinamen aus dem Pfad und speichert ihn in der Variable MATCHED_FILENAME
    SetEnvIf Request_URI "([^/]+\.gz)$" MATCHED_FILENAME=$1
    
    # Setzt den Content-Disposition Header mit dem extrahierten Dateinamen
    Header set Content-Disposition "attachment; filename=\"%{MATCHED_FILENAME}e\"" env=MATCHED_FILENAME
    
    # Sicherstellen, dass der Content-Type für Gzip korrekt ist
    ForceType application/gzip
</FilesMatch>

Then, use your webserver URL in OpnSense's Firewall->Aliases->GeoIP settings. You may have to use the "Actions" button to actually apply the setting.
