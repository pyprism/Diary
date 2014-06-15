<?php
/**
 * Created by PhpStorm.
 * User: prism
 * Date: 5/30/14
 * Time: 7:09 PM
 */

class Content extends Eloquent {
    protected $table = 'content';

    protected $fillable;

    public function User(){
        return $this->belongsTo('User');
    }
}