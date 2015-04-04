<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class Post extends Model {

	protected $timestamp = false;
    protected $table = 'posts';

    /*
     * Relationship
     */

    public function user() {
        $this->belongsTo('App\User');
    }

    public function tag() {
        $this->hasMany('App\Tag');
    }
}
