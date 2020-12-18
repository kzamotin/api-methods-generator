package sample;
use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use Encode;
use Data::Dumper;

sub new {
    my $class = shift;
	
    my $self = bless {
            url => shift,
			token => shift,
			delay => shift,
            sortBy => '',
            offset => '',
            limit => ''
        }, $class;
    
    $self->{ua} = LWP::UserAgent->new;
    $self->{ua}->cookie_jar( {} );
	
    return $self;
}
sub build_json {
	my $self = shift;
    my $methodName = shift;    
    my $params     = shift;
    my %paramsHash = %$params;
    
    my %jsonObject = ( 'jsonrpc' => '2.0', 'method' => $methodName, 'token' => $self->{token}, 'params' => \%paramsHash, 
    'filter' => {'sortBy' => $self->{sortBy}, 'offset' => $self->{offset}, 'limit' => $self->{limit}} );
    
    my $json = decode_utf8( (encode_json \%jsonObject));
    
    return $json;
}

sub postApi {
     my $self       = shift;
     my $method     = shift;
     my $params     = shift;
     select(undef, undef, undef, $self->{delay});
	 
     my $req = HTTP::Request->new(POST => $self->{url});
     $req->header('content-type' => 'application/json');
      
    my $post_data = encode_utf8( $self->build_json( $method, $params ));
    $req->content($post_data);
	print Dumper($post_data);
 
    my $resp = $self->{ua}->request($req);
    
    if ($resp->is_success) {
       my $message =  $resp->decoded_content;
      
       my $responseDecoded= decode_json($message);
      
       return undef if $resp->code ne 200;
       return undef if not defined $responseDecoded->{result} or defined $responseDecoded->{error};       
       return undef if ($responseDecoded->{result} eq "");
       $self->{extrainfo}= $responseDecoded->{resultExtraInfo};
       return $responseDecoded->{result};
    }
    
    
    return undef;
}
sub genericFilter {
	my $self = shift;
	my $sortBy = shift;
	my $offset = shift;
	my $limit = shift;

	$self->{sortBy} = $sortBy;
    $self->{offset} = $offset;
    $self->{limit} = $limit;

}
   
sub genericFilterClear {
	my $self = shift;
    $self->{sortBy} = '';
    $self->{offset} = '';
    $self->{limit} = '';
}
	
sub getExtraInfo {
	my $self = shift;
    return $self->{extrainfo};
} 


sub get_system_info {  
	my $self      = shift;
	my %params = ();
	my $result = $self->postApi('get_system_info', \%params);
	return $result;
}
sub get_status {  
	my $self      = shift;
	my %params = ();
	my $result = $self->postApi('get_status', \%params);
	return $result;
}
sub set_status {  
	my $self      = shift;
	my $status=shift;
	my $mood=shift;
	my %params = ('status' => $status,'mood' => $mood);
	my $result = $self->postApi('set_status', \%params);
	return $result;
}
sub make_payment {  
	my $self      = shift;
	my $from_wallet=shift;
	my $to_wallet=shift;
	my $amount=shift;
	my $comment=shift;
	my %params = ('from_wallet' => $from_wallet,'to_wallet' => $to_wallet,'amount' => $amount,'comment' => $comment);
	my $result = $self->postApi('make_payment', \%params);
	return $result;
}
1;