################################################################################
# Shell function for safe use of `apparition apparate`.
# Arguments:
#     $1: The destination name passed to `apparition apparate`
# Outputs:
#     Writes error messages to STDERR.
################################################################################
function apparate() {
    output=$(apparition apparate "$@")
    if [ $? = 0 ]; then
        eval $output
    else
        apparition print-error "$output"
    fi
}
