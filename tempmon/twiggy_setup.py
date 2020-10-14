from twiggy import add_emitters, outputs, levels, filters, formats, emitters, log

log_levels = {0: levels.NOTICE, 1: levels.INFO, 2: levels.DEBUG}


def twiggy_setup(logfile=None, verbosity=0):
    if logfile:
        main_output = outputs.FileOutput(logfile, format=formats.line_format)
    else:
        main_output = outputs.StreamOutput(format=formats.line_format)

    add_emitters(
        # (name, min_level, filter, output)
        ("main", log_levels[verbosity], None, main_output)
    )

    log.name("twiggy_setup").fields(file=logfile, level=log_levels[verbosity]).debug(
        f"Twiggy configured with log level {log_levels[verbosity]}."
    )
