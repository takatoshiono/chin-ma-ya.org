#!/usr/bin/env perl

use strict;
use warnings;

use DBI;
use Encode ();
use FindBin;
use Getopt::Long;

use lib "$FindBin::Bin/../lib";
use Chinmaya::Scraper;

my %opts;
if (!GetOptions(\%opts,
    'dbfile=s',
    )) {
    exit(1);
}

if ($opts{dbfile}) {
    my $dbh = DBI->connect("dbi:SQLite:dbname=$opts{dbfile}", '', '');
    do_work($dbh);
    $dbh->disconnect;
}
else {
    print "$0 --dbfile /path/to/db\n";
}

sub do_work {
    my $dbh = shift;

    my $areas = fetch_areas($dbh);

    my $scraper = Chinmaya::Scraper->new();

    eval {
        AREA:
        foreach my $area (@$areas) {
            print STDERR "scraping $area->{name}...\n";

            my $is_exists = fetch_shops($dbh, $area->{id});

            my $shops = eval {
                $scraper->get_shops($area->{initial_words});
            };
            if ($@) {
                print STDERR "failed to scrape shops($area->{name}): $@";
                next AREA;
            }

            ADD_SHOP:
            foreach my $shop (@$shops) {
                my $shop_name = Encode::encode('utf-8', $shop->{name});
                unless (delete $is_exists->{$shop_name}) {
                    print STDERR "Queue shop(for add): $shop_name\n";
                    add_queue($dbh, {
                        method => 'add',
                        area_id => $area->{id},
                        area_name => $area->{name},
                        shop_name => $shop_name,
                        address => $shop->{address},
                        latitude => $shop->{latitude},
                        longitude => $shop->{longitude},
                        extra => $shop->{extra},
                    });
                }
            }

            DELETE_SHOP:
            foreach my $shop (values %$is_exists) {
                print STDERR "Queue shop(for delete): $shop->{name}\n";
                add_queue($dbh, {
                    method => 'delete',
                    area_id => $area->{id},
                    area_name => $area->{name},
                    shop_id => $shop->{id},
                    shop_name => $shop->{name},
                    address => $shop->{address},
                    latitude => $shop->{latitude},
                    longitude => $shop->{longitude},
                    extra => $shop->{extra},
                });
            }
        }
    };
    if ($@) {
        warn "Transaction failed: $@";
    }
}

sub fetch_areas {
    my $dbh = shift;

    return $dbh->selectall_arrayref(
        'SELECT * FROM areas WHERE deleted_at IS NULL ORDER BY id ASC',
        { Slice => {} },
    );
}

sub fetch_shops {
    my ($dbh, $area_id) = @_;

    my $sql = <<'EOS';
SELECT * FROM shops WHERE area_id = ? AND deleted_at IS NULL ORDER BY id ASC
EOS

    return $dbh->selectall_hashref($sql, 'name', undef, $area_id);
}

sub add_queue {
    my ($dbh, $shop) = @_;

    my $sql = <<'EOS';
INSERT INTO queue_shop (
    method, area_id, area_name, shop_id, shop_name, address, latitude, longitude, extra, created_at
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now')
)
EOS

    my $sth = $dbh->prepare($sql);
    $sth->execute(
        $shop->{method},
        $shop->{area_id},
        $shop->{area_name},
        $shop->{shop_id},
        $shop->{shop_name},
        $shop->{address},
        $shop->{latitude},
        $shop->{longitude},
        $shop->{extra},
    );
}

