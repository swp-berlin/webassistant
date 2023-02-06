/* eslint-disable import/no-extraneous-dependencies */

const path = require('path');
const {StatsWriterPlugin} = require('webpack-stats-plugin');

class AssetsMapWriterPlugin extends StatsWriterPlugin {

    constructor(filename) {
        super({fields: ['assets'], filename});

        this.mapping = {};

        // @ts-ignore
        this.opts.transform = this.transform.bind(this);
    }

    transform(stats) {
        stats.assets.forEach(({name}) => {
            const pathObject = path.parse(name);

            if (pathObject.name.indexOf('.') > 0) {
                /* removes the last bit of the filename which should be the hash */
                pathObject.name = pathObject.name.split('.').slice(0, -1).join('.');
                pathObject.base = null;
            }

            const key = path.format(pathObject);

            this.mapping[key] = name;
        });

        return JSON.stringify(this.mapping, null, 2);
    }

}

module.exports = AssetsMapWriterPlugin;
