#!/usr/bin/env perl

use strict;
use warnings;

my $insert;
while (<>) {
    if (/^INSERT/) {
        $insert = $_;
        last;
    }
}

my @values = $insert =~ /\((.+?)\)/g;
print STDERR scalar(@values), "\n";

foreach my $value (@values) {
    print "INSERT INTO shops VALUES($value);\n";
}

