try:
    import collectd
    from .collect import run_collectd
    run_collectd(collectd)
except Exception as e:
    pass
