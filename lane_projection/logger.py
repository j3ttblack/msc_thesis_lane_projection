import logging
import time
from datetime import timedelta
import math
import os 
from pathlib import Path


def setup_logger(base_name="debug_logger"):
    '''
    Initialize and return a reusable Python logger.

    Args:
        base_name (str, optional): Name of the logger instance. Default is "debug_logger".

    Returns:
        logger (logging.Logger): Logger object.
    '''
    logger = logging.getLogger(base_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # prevent double logging
    return logger



def switch_log_file(logger, log_file_path, seq_id=None, overwrite=True, log_console=False):
    '''
    Switch to a new logger, clearing handlers and creating a new file.

    Args:
        logger (logging.Logger): Existing logger instance to replace.
        log_file_path (str): Directory for new log file.
        seq_id (str / int, optional): Log file is named "log_<seq_id>.log"; otherwise keeps logger name.
        overwrite (bool, optional): Whether to overwrite (True, default) or append (False) to an existing log file.
        log_console (bool): Whether to also output logs to the terminal console. Default is false.

    Outputs:
        Creates or appends to a log file on disk. Optional console logging.
    '''
    
    os.makedirs(Path(log_file_path), exist_ok=True)
    if seq_id is not None:
        log_file = os.path.join(log_file_path, f"log_{seq_id}.log")
    else:
        log_file = os.path.join(log_file_path, f"{logger.name}.log")

    # Remove old handlers
    for h in logger.handlers[:]:
        logger.removeHandler(h)
        h.close()

    mode = "w" if overwrite else "a"
    fh = logging.FileHandler(log_file, mode=mode)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if log_console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)

    # Initialize timer storage
    logger._timer_start = None

    logger.info(f"Logging started")



def start_timer(logger):
    '''
    Start or reset an internal timer on the logger.

    Args:
        logger (logging.Logger): Logger to restart timer.
    '''
    logger._timer_start = time.time()



def stop_timer(logger, solution, total_lanes=0, calc_lane_time=True):
    '''
    Stop the logger timer and record the (formatted) elapsed time (and optional average time) in the log file.

    Inputs:
        logger (logging.Logger): Logger.
        solution (str / int): Identifier for the solution/method being timed.
        total_lanes (int, optional): Number of lanes processed, to compute avg time/lane. Does not calculate if not specified.
        calc_lane_time (bool, optional): Whether to compute and log per-lane timing information. Default is true.

    Outputs:
        Logs a formatted timing message to the logger's file (and console if specified).

    Returns:
        elapsed_sec (float): Total elapsed time in seconds between start_timer() and stop_timer().
    '''
    if logger._timer_start is None:
        raise RuntimeError("Timer was not started. Call start_timer(logger) first.")
    
    stop_time = time.time()
    elapsed_sec = stop_time - logger._timer_start
    logger._timer_start = None  # reset for next timing

    # Round to ceiling milliseconds (minimum 0.01s)
    ceil_elapsed_sec = max(elapsed_sec, 0.01)
    round_elapsed_sec = math.ceil(ceil_elapsed_sec * 100) / 100  # ceil to 0.01 s

    # Convert to H:M:S.ms format
    def sec_to_hms(sec):
        td = timedelta(seconds=sec)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        ms = int((td.total_seconds() - total_seconds) * 100)
        return hours, minutes, seconds, ms

    hours, minutes, seconds, ms = sec_to_hms(round_elapsed_sec)
    elapsed_str = f"{hours}:{minutes:02d}:{seconds:02d}.{ms:02d}"
    full_message = f"Solution {solution}:\tElapsed time: {elapsed_str}"

    if calc_lane_time:
        if total_lanes != 0:
            round_average_sec = math.ceil((ceil_elapsed_sec/total_lanes) * 100) / 100
            hours, minutes, seconds, ms = sec_to_hms(round_average_sec)
            avg_elapsed_str = f"{hours}:{minutes:02d}:{seconds:02d}.{ms:02d}"
            full_message += f"\tAvg Time [x{total_lanes} lanes]: {avg_elapsed_str}"
        else:
            full_message += "\tAll files already processed."

    logger.info(full_message)

    return elapsed_sec
