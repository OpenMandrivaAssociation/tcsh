# color-ls initialization
set COLORS=/etc/DIR_COLORS
eval `dircolors -c /etc/DIR_COLORS`
test -f ~/.dircolors && eval `dircolors -c ~/.dircolors` && set COLORS=~/.dircolors
test -f ~/.dir_colors && eval `dircolors -c ~/.dir_colors` && set COLORS=~/.dir_colors

egrep -qi "^COLOR.*none" $COLORS

if ( $? != 0 ) then
alias ls 'ls --color=tty'
endif
