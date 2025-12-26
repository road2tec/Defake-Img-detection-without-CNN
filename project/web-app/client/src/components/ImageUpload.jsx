import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';

const ImageUpload = ({ onImageUpload }) => {
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles?.length > 0) {
            const file = acceptedFiles[0];
            // Create preview URL
            const previewUrl = URL.createObjectURL(file);
            onImageUpload(file, previewUrl);
        }
    }, [onImageUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.jpg', '.png']
        },
        multiple: false
    });

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
            style={{
                width: '100%',
                height: '300px',
                border: isDragActive ? '2px dashed var(--accent)' : '2px dashed var(--glass-border)',
                background: isDragActive ? 'rgba(6, 182, 212, 0.1)' : 'var(--glass-bg)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
            }}
            {...getRootProps()}
        >
            <input {...getInputProps()} />
            <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
                <div style={{
                    width: '64px',
                    height: '64px',
                    borderRadius: '50%',
                    background: 'rgba(255, 255, 255, 0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '0.5rem'
                }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--primary)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                </div>
                <div>
                    <p style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.25rem', color: 'white' }}>Upload Face Image</p>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                        {isDragActive
                            ? "Drop the image here..."
                            : "Drag & drop or click to select"}
                    </p>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '1rem', opacity: 0.7 }}>Supports JPG, PNG, JPEG</p>
                </div>
            </div>
        </motion.div>
    );
};

export default ImageUpload;
