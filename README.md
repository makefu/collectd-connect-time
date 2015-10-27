# TCP Connect Time Plugin

Returns the time required to connect to hostname[:port]

# Collectd Configuration

      LoadPlugin python

      <Plugin python>
          ModulePath "/usr/lib/python2.7/dist-packages/"
          Import "collectd_connect_time"
          <Module collectd_connect_time>
              target "google.de" "web.de" "aol.com"
          </Module>
      </Plugin>

- this results in values stored at `<hostname>.connect-time-<target[1]>.response_time-max`

# License

See `LICENSE`
