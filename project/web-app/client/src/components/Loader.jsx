import React from 'react';

const Loader = () => {
    return (
        <div className="flex flex-col items-center justify-center p-8">
            <span className="loader"></span>
            <p className="mt-4 text-gray-300 animate-pulse">Analyzing pixel patterns...</p>
        </div>
    );
};

export default Loader;
