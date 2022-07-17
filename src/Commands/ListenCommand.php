<?php

namespace Liostech\Callbackin\Commands;

use Illuminate\Console\Command;
use PhpMqtt\Client\MqttClient;

class ListenCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'callbackin:listen';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Listen for callback requests';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $path = env('CALLBACKIN_PUBLIC_PATH', 'callback');
        $endpoint = env('CALLBACKIN_LOCAL_ENDPOINT', 'http://localhost:8000/callback');
        $this->info("Listening for callback: $path");
        $mqtt = new MqttClient(
            "mqtt.eclipseprojects.io",
            1883,
            "callbackin-" . uniqid()
        );
        $mqtt->connect();
        $mqtt->subscribe($path, function ($topic, $message) use ($endpoint) {
            $this->callHttp($endpoint, $message);
        }, 0);
        $mqtt->loop(true);
        $mqtt->disconnect();
    }

    public function callHttp($endpoint, $message)
    {
        $jsonData = json_decode($message, true);
        $headerJson = $jsonData['headers'];
        $body = $jsonData['body'];
        $headers = [];
        foreach ($headerJson as $key => $value) {
            if ($key == 'Content-Length') {
                $headers[] = $key . ': ' . strlen(json_encode($body));
            } else {
                $headers[] = $key . ': ' . $value;
            }
        }
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $endpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 1);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        $this->info("Sending callback to: $endpoint");
        $result = curl_exec($ch);
        curl_close($ch);
        $this->info("Response: $result");
    }
}
