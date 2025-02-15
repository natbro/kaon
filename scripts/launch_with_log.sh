#!/bin/zsh
self=`realpath $0`
self=`dirname $self`
crossover_log="$self/crossover_log.txt"
echo "--" `date` "---------------" >> "$crossover_log"
echo "args:|" "$@" "|" >> "$crossover_log"
env >> "$crossover_log"
echo "------------------------------------" >> "$crossover_log"
"$self/launch_crossover.sh" $@ >> "$crossover_log" 2>&1
