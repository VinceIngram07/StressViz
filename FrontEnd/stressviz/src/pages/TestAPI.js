import React, { useState } from 'react';

const BreathingExercises = () => {
    const [showVideos, setShowVideos] = useState(false); // Add this state variable

    // List of predefined YouTube video IDs for breathing exercises
    const breathingVideos = [
        { title: 'Deep Breathing Exercise', videoId: 'Dx112W4i5I0' },
        { title: 'Stressing Video', videoId: 'CFV7Xjs_240' },
        // Add more videos as needed
    ];

    return (
        <div>
            <h1>Videos</h1>
            <button onClick={() => setShowVideos(!showVideos)}> {/* Add this button */}
                {showVideos ? 'Hide Videos' : 'Show Videos'}
            </button>
            {showVideos && (
                <div>
                    {breathingVideos.map((video) => (
                        <div key={video.videoId}>
                            <h2>{video.title}</h2>
                            <iframe
                                title={video.title}
                                width="560"
                                height="315"
                                src={`https://www.youtube.com/embed/${video.videoId}`}
                                frameBorder="0"
                                allowFullScreen
                            ></iframe>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default BreathingExercises;