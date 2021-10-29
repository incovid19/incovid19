def StatusMsg(StateCode: str, date: str, StatusCode: str, statusMessage: str, program: str = "GetSource") -> None:
    """
    Routine to write the status of Program1(or GetSource) for each state

    StateCode: State Code (Ex. Karnataka KA)
    date: Current Date in format YYYY-MM-DD
    program: Name of the calling program
    StatusCode: Whether there is an error or its ok (OK/ERR)
    statusMessage: Text describing the status of the call

    """
    if not StateCode:
        print("No State Code!")
        log_message = "Verify Calling program, State Code missing!"
    elif not date:
        print("No date!")
        log_message = "Verify Calling program, Date missing!"
    elif not StatusCode:
        print("Status Code missing!")
        log_message = "Verify Calling program, Status Code missing!"
    elif not statusMessage:
        print("No status message!")
        log_message = "Verify Calling program, status message missing!"
    else:
        log_message = StateCode + "|" + date + "|" + program + "|" + StatusCode + "|" + statusMessage + "\n"
    file_name = "../LOG/" + date + "/" + StateCode + ".log"
    f = open(file_name, "w+")
    f.write(log_message)
