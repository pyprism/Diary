<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model {

    protected $timestamp = false;
    protected $table = 'tags';

    /*
     * Relationship
     */

    public function posts() {
        $this->belongsTo('App\Post');
    }
}
