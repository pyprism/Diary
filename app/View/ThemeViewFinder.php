<?php
/**
 * Created by PhpStorm.
 * User: prism
 * Date: 1/11/16
 * Time: 9:00 AM
 */

namespace app\View;

use Illuminate\View\FileViewFinder;

class ThemeViewFinder extends FileViewFinder{

    protected $activeTheme;

    protected $basePath;

    public function setBasePath($path) {
        $this->basePath = $path;
    }

    public function setActiveTheme($theme) {
        $this->activeTheme = $theme;

        array_unshift($this->paths, $this->basePath. '/'. $theme. '/views');
    }
}