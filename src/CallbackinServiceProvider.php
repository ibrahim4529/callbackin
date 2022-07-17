<?php

namespace Liostech\Callbackin;

use Illuminate\Support\ServiceProvider;
use Liostech\Callbackin\Commands\ListenCommand;

class CallbackinServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->registerConfig();
    }

    /**
     * Boot the authentication services for the application.
     *
     * @return void
     */
    public function boot()
    {
        if($this->app->runningInConsole()){
            $this->registerCommand();
            $this->publishConfig();
        }
    }


    public function registerConfig()
    {
        $this->mergeConfigFrom(
            __DIR__.'/../config/callbackin.php', 'callbackin'
        );
    }

    public function publishConfig()
    {
        $this->publishes([
            __DIR__.'/../config/callbackin.php' => config_path('callbackin.php'),
        ], 'callbackin-config');
    }


    public function registerCommand()
    {
        $this->commands([
            ListenCommand::class,
        ]);
    }

}
