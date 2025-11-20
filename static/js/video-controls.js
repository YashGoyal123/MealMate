// Video Controls JavaScript
// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Video player controls
    const video = document.getElementById('recipeVideo');
    
    // Only add controls if video exists
    if (!video) {
        console.log('No video element found');
        return;
    }
    
    console.log('✅ NEW CODE LOADED - Video element found, setting up controls...');
    
    const playPauseBtn = document.getElementById('playPauseBtn');
    const muteBtn = document.getElementById('muteBtn');
    const skipForwardBtn = document.getElementById('skipForwardBtn');
    const skipBackwardBtn = document.getElementById('skipBackwardBtn');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    
    // Skip Forward Function
    function skipForward(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        console.log('✅ SKIP FORWARD - Current time:', video.currentTime);
        
        const newTime = video.currentTime + 10;
        console.log('✅ SKIP FORWARD - Setting to:', newTime);
        
        video.currentTime = newTime;
        
        setTimeout(() => {
            console.log('✅ SKIP FORWARD - After 50ms, currentTime is:', video.currentTime);
        }, 50);
    }
    
    // Skip Backward Function
    function skipBackward(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        console.log('✅ SKIP BACKWARD - Current time:', video.currentTime);
        
        const newTime = Math.max(0, video.currentTime - 10);
        console.log('✅ SKIP BACKWARD - Setting to:', newTime);
        
        video.currentTime = newTime;
        
        setTimeout(() => {
            console.log('✅ SKIP BACKWARD - After 50ms, currentTime is:', video.currentTime);
        }, 50);
    }
    
    // Toggle Play/Pause Function
    function togglePlayPause(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        console.log('Toggle play/pause clicked');
        if (video.paused) {
            video.play();
            if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fas fa-pause me-1"></i>Pause';
        } else {
            video.pause();
            if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fas fa-play me-1"></i>Play';
        }
    }
    
    // Toggle Mute Function
    function toggleMute(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        video.muted = !video.muted;
        if (muteBtn) {
            if (video.muted) {
                muteBtn.innerHTML = '<i class="fas fa-volume-mute me-1"></i>Unmute';
            } else {
                muteBtn.innerHTML = '<i class="fas fa-volume-up me-1"></i>Mute';
            }
        }
    }
    
    // Toggle Fullscreen Function
    function toggleFullscreen(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        console.log('Toggle fullscreen clicked');
        if (!document.fullscreenElement) {
            if (video.requestFullscreen) {
                video.requestFullscreen();
            } else if (video.webkitRequestFullscreen) {
                video.webkitRequestFullscreen();
            } else if (video.msRequestFullscreen) {
                video.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }
    
    // Add event listeners to buttons
    if (skipForwardBtn) {
        skipForwardBtn.addEventListener('click', skipForward);
    }
    if (skipBackwardBtn) {
        skipBackwardBtn.addEventListener('click', skipBackward);
    }
    if (playPauseBtn) {
        playPauseBtn.addEventListener('click', togglePlayPause);
    }
    if (muteBtn) {
        muteBtn.addEventListener('click', toggleMute);
    }
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', toggleFullscreen);
    }
    
    // Make functions global for keyboard shortcuts
    window.skipForward = skipForward;
    window.skipBackward = skipBackward;
    window.togglePlayPause = togglePlayPause;
    window.toggleMute = toggleMute;
    window.toggleFullscreen = toggleFullscreen;
    
    // Update play/pause button when video state changes
    video.addEventListener('play', function() {
        if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fas fa-pause me-1"></i>Pause';
    });
    
    video.addEventListener('pause', function() {
        if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fas fa-play me-1"></i>Play';
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Only if video is in focus or no input is focused
        if (document.activeElement.tagName === 'INPUT' || 
            document.activeElement.tagName === 'TEXTAREA') {
            return;
        }
        
        switch(e.key) {
            case ' ':
                e.preventDefault();
                window.togglePlayPause();
                break;
            case 'ArrowRight':
                e.preventDefault();
                window.skipForward();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                window.skipBackward();
                break;
            case 'm':
            case 'M':
                e.preventDefault();
                window.toggleMute();
                break;
            case 'f':
            case 'F':
                e.preventDefault();
                window.toggleFullscreen();
                break;
        }
    });
});
