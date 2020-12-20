unit sub MAIN(Str $alku, Str $eka = "Draco", Str $ekalle = "Dracolle", Str $toka = "Harry", Str $tokalle = "Harrylle");

my $sampler = run "python3", "sample-model.py", "sp-aooo-10k", "aooo", "--transformerxl", :in, :out;
$sampler.in.put: "/n 50";
$sampler.in.put: "/repe 0.7";
sub predict(Str $prompt is copy, :$with-prompt --> Str) {
	$prompt .= trim-leading;
	$sampler.in.put: $prompt;
	$_ = $sampler.out.get;
	s/^ "> "+//;
	s:g/\x1b .*? m//;
	$_ .= substr($prompt.chars+1);
	s:g/"”"/"/;
	#note "$prompt --> $_";
	$with-prompt ?? "$prompt$_" !! $_
}

sub fix-punctuation(Str $text is copy --> Str) {
	if $text ~~ / <[!?]> $/ {
		qq["$text"]
	} else {
		$text ~~ s/ "." $//;
		qq["$text",]
	}
}

my Str %äänet = $eka => "hy_fi_mv_diphone", $toka => "suo_fi_lj_diphone";

sub simulate-dialog(Str $previous, Str $puhuja, Str $kuuntelijalle --> Str) {
	my $prompt = $previous ?? qq[$previous br $puhuja sanoo $kuuntelijalle: "] !! qq[$puhuja sanoo $kuuntelijalle: "];
	predict($prompt) ~ '"' ~~ /^ (<-["]>*) ('"' | " br")/;
	my $output = $0.trim;
	say "$puhuja: $output";
	my $synth = run "festival", :in;
	$synth.in.write: qq[(%äänet{$puhuja})(SayText "$output")].encode("ISO-8859-1");
	$synth.in.close;
	qq[$prompt$output"]
}

my $conversation = $alku;

for ^5 {
	$conversation = simulate-dialog($conversation, $eka, $tokalle);
	$conversation = simulate-dialog($conversation, $toka, $ekalle);
}

say $conversation;

$sampler.in.close;
$sampler.out.close;
