import os from 'os'
import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'
import boxen from 'boxen'
import chalk from 'chalk'
import { Board } from 'pi-home-core'

import { api } from './api'

export const server = () => {
  // app setup
  const app: express.Application = express()
  const port: number = 5000

  app.use(helmet())
  app.use(express.json())
  app.use(morgan('common'))

  // db setup
  const lowdb = require('lowdb')
  const FileSync = require('lowdb/adapters/FileSync')

  const adapter = new FileSync('db.json')
  const db = lowdb(adapter)

  db.defaults({
    devices: [],
    dependencies: [],
  }).write()

  // board setup
  const board = new Board()
  board.setConfig({
    devices: db.get('devices').value(),
    dependencies: db.get('dependencies').value(),
  })

  // routes setup
  app.get('/', (req, res) => {
    res.send('Welcome to raspberry-pi-home!')
  })

  // /api router
  app.use('/api', api(db, board))

  app.use((err: any, req: any, res: any, next: any) => {
    if (process.env.DEBUG) {
      // eslint-disable-next-line no-console
      console.error(err.stack)
    }
    res.status(500).send(err.message)
  })

  app.listen(port, () => {
    const interfaces = os.networkInterfaces()

    const getNetworkAddress = () => {
      for (const name of Object.keys(interfaces)) {
        // @ts-ignore TS2532
        for (const localInterface of interfaces[name]) {
          const { address, family, internal } = localInterface
          if (family === 'IPv4' && !internal) {
            return address
          }
        }
      }
    }

    const localAddress = `http://localhost:${port}`
    const networkAddress = getNetworkAddress()

    let message = chalk.green('Server running!')

    const prefix = networkAddress ? '- ' : ''
    const space = networkAddress ? '            ' : '  '

    message += `\n\n${chalk.bold(`${prefix}Local:`)}${space}${localAddress}`

    if (networkAddress) {
      message += `\n${chalk.bold('- On Your Network:')}  http://${networkAddress}:${port}`
    }

    // eslint-disable-next-line no-console
    console.log(boxen(message, {
      padding: 1,
      borderColor: 'green',
      margin: 1,
    }))
  })
}
