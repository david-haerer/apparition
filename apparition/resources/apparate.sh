################################################################################
# Shell function for safe use of `apparition apparate`.
# Arguments:
#     $1: The destination name passed to `apparition apparate`
#         If the value is `--help` only the help text is shown.
#         Otherwise the command is executed with `eval`.
# Outputs:
#     Writes error messages to STDERR.
################################################################################
function apparate() {
    destination="$1"
    if [ $destination = "--help" ]; then
        apparition apparate --help
        return
    fi

    output=$(apparition apparate --called-from-shell-function "$1")

    if [ $? = 0 ]; then
        eval $output
    else
        apparition print-error "$output"
    fi
}
